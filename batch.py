#!/usr/bin/env python3
"""cek saldo banyak alamat EVM dari file, 1 request per alamat"""
import json
import sys
import urllib.request

RPC = "https://eth.llamarpc.com"


def get_balance(addr: str) -> float | None:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_getBalance",
                       "params": [addr, "latest"]}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        res = json.load(r)
    if "result" not in res:
        return None
    return int(res["result"], 16) / 1e18


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "addresses.txt"
    try:
        addrs = [l.strip() for l in open(path) if l.strip()]
    except FileNotFoundError:
        sys.exit(f"file {path} gak ketemu")
    total = 0
    for a in addrs:
        bal = get_balance(a)
        total += bal or 0
        print(f"{a}  {bal:.6f} ETH" if bal is not None else f"{a}  error")
    print(f"total: {total:.6f} ETH ({len(addrs)} alamat)")


if __name__ == "__main__":
    main()
