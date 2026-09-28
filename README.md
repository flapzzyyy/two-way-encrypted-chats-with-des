# Two-Way Encrypted Chat (Manual DES)

| Name | NRP |
|---|---|
| Yoseph Kevin Hendrata | 5025241146 |

A simple chat between two devices (sender ⇄ receiver) over TCP.
Every message is encrypted with **DES implemented manually** before it is sent, and decrypted on the other side.

## Key

```python
KEY = "T1KIB146"
```

The key is stored in `peer.py` on **both** devices and is **never sent** over the network.
Only the ciphertext (in hex) travels over the network.

## Method

```
Sender: message -> padding -> DES-CBC(key, random IV) -> hex -> send over TCP
Receiver: hex -> split off the IV -> DES-CBC decrypt(key) -> remove padding -> message
```

- **Padding (PKCS#7):** the message is padded to a multiple of 8 bytes, since DES works on 8-byte blocks.
- **IV:** 8 random bytes, new for every message, sent along at the front of the ciphertext (the first 16 hex characters).
- **CBC:** each block is XORed with the previous ciphertext block before DES.

## Setup

Prepare an Ubuntu host and an Ubuntu VM, both with Python 3 installed.

1. Set the VM network adapter to **Bridged** or **Host-only**.
2. Check each side's IP: `ip -br a`, then test with `ping <other-side-IP>`.
3. If `ufw` is enabled on the server: `sudo ufw allow 5000/tcp`
4. Copy `des.py` and `peer.py` to the VM.

## Run

Host (server):
```bash
python3 peer.py server
```

VM (client):
```bash
python3 peer.py <host-ip>
```

Type a message and press Enter. Both sides can send at any time. Type `/quit` to exit.

Example output:
```
[OUT] Message : Hello from Host
[OUT] ciphertext : a7b87528c2b2f7b092f79aeaacce6ee71bcb1484e0a2da2b

[IN] ciphertext : 5eaf297fcf87b718cd5b94684c4ea06bd292d969634f38ba21a5ea4a604665c7
[IN] Message : Hello from VM
```

## Sources

- NIST, *FIPS PUB 46-3: Data Encryption Standard (DES)*, 1999. https://csrc.nist.gov/files/pubs/fips/46-3/final/docs/fips46-3.pdf
- Wikipedia, *DES supplementary material* (IP, FP, E, P, PC-1, PC-2, rotation and S-box tables). https://en.wikipedia.org/wiki/DES_supplementary_material
- W. Stallings, *Cryptography and Network Security: Principles and Practice*, chapter on DES.

## License

Copyright (c) 2026 Yoseph Kevin Hendrata. All rights reserved. See [LICENSE](LICENSE).
