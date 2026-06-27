import json, os, hashlib

repos = [
   "/Users/g.bogans/Downloads/FARD_v0.5",
   "/Users/g.bogans/Downloads/FARD Prim",
   "/Users/g.bogans/Downloads/ESCS",
   "/Users/g.bogans/Downloads/FARD_ISA",
   "/Users/g.bogans/Downloads/Music Theory in FARD",
   "/Users/g.bogans/Downloads/Fard Dinar",
   "/Users/g.bogans/Downloads/Azim Trial",
]

# 129-token character vocab — same as azim_trial/tokenizer
special = ["<PAD>", "<UNK>", "<BOS>", "<EOS>"]
chars = list(" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + \
       list(".,;:!?\"'`-_+=<>()[]{}|/\\@#$%^&*~\n\t")
vocab = (special + chars)[:129]
char_to_id = {c: i for i, c in enumerate(vocab)}

def tokenize(text):
   ids = [2]  # BOS
   for c in text:
       ids.append(char_to_id.get(c, 1))  # UNK=1
   ids.append(3)  # EOS
   return ids

def sha256(text):
   return "sha256:" + hashlib.sha256(text.encode()).hexdigest()

records = []
skipped = 0
repo_counts = {}

for repo_path in repos:
   repo_name = os.path.basename(repo_path)
   repo_counts[repo_name] = 0
   for root, dirs, files in os.walk(repo_path):
       # skip hidden, git, out, __pycache__
       dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('out', '__pycache__', 'node_modules')]
       for fname in files:
           if not fname.endswith('.fard'):
               continue
           fpath = os.path.join(root, fname)
           try:
               src = open(fpath, encoding='utf-8', errors='replace').read()
               if len(src.strip()) == 0:
                   skipped += 1
                   continue
               tokens = tokenize(src)
               # skip if max token ID exceeds vocab
               if max(tokens) >= 129:
                   skipped += 1
                   continue
               # skip very short files (< 10 tokens)
               if len(tokens) < 12:
                   skipped += 1
                   continue
               records.append({
                   "kind": "fard_source",
                   "lang": "fard",
                   "repo": repo_name,
                   "path": fpath,
                   "source_sha256": sha256(src),
                   "token_count": len(tokens),
                   "tokens": tokens
               })
               repo_counts[repo_name] += 1
           except Exception as e:
               skipped += 1

os.makedirs("out/fard_mega_corpus", exist_ok=True)
out_path = "out/fard_mega_corpus/train_shard.jsonl"
with open(out_path, "w") as f:
   for r in records:
       f.write(json.dumps(r) + "\n")

print(f"Total records: {len(records)}")
print(f"Total tokens: {sum(r['token_count'] for r in records):,}")
print(f"Skipped: {skipped}")
print(f"Max token ID: {max(t for r in records for t in r['tokens'])}")
print()
print("Per-repo breakdown:")
for repo, count in repo_counts.items():
   tokens = sum(r['token_count'] for r in records if r['repo'] == repo)
   print(f"  {repo:35s}: {count:4d} files  {tokens:8,} tokens")
