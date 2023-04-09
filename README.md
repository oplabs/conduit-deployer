# conduit-deployer

Seaport conduit deployer

## Setup

```bash
python3 -m venv /path/to/venv
source /path/to/venv/bin/activate
pip install -r requirements.lock.txt
```

## Deploy

```bash
ape run scripts/deploy.py --network polygon:mainnet -o OWNER -a DEPLOYER
```
