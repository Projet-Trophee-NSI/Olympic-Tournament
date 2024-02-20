import hashlib

def hash(mdp : str) -> str:
    h=hashlib.new("SHA256")
    h.update(mdp.encode())
    mdp_hash=h.hexdigest()
    return mdp_hash