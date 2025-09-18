import os

# Get current PATH
path_env = os.environ.get('PATH', '')
path_sep = os.pathsep

# Split, deduplicate while preserving order
seen = set()
deduped_paths = []
for p in path_env.split(path_sep):
    if p not in seen:
        seen.add(p)
        deduped_paths.append(p)

# Join back into PATH string
new_path = path_sep.join(deduped_paths)

print("New deduplicated PATH:")
print(new_path)

# Optional: set it for the current process (does not affect the system)
# os.environ['PATH'] = new_path
