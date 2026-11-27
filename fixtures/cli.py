"""Small reproducible CLI fixture; reports are assertions, not remote attestation."""
import argparse
p = argparse.ArgumentParser()
p.add_argument('--name', default='developer')
a = p.parse_args()
print('Hello, ' + a.name + '!')
