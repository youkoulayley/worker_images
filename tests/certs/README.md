# Generate certificate for NATS streaming server

Do not use the certificate present on this repo !
There are here only to do some tests.

## CA
```bash
cat > ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "worker_images": {
        "usages": ["signing", "key encipherment", "server auth", "client auth"],
        "expiry": "87600h"
      }
    }
  }
}
EOF

cat > ca-csr.json <<EOF
{
  "CN": "Worker_images",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "FR",
      "L": "Bordeaux",
      "O": "worker_images",
      "OU": "CA",
      "ST": "Gironde"
    }
  ]
}
EOF

cfssl gencert -initca ca-csr.json | cfssljson -bare ca
```


## Client
```bash
cat > client-csr.json <<EOF
{
  "CN": "worker_images",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "FR",
      "L": "Bordeaux",
      "O": "worker_images",
      "OU": "CA",
      "ST": "Gironde"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -hostname=127.0.0.1,nats-streaming-tls \
  -profile=worker_images \
  client-csr.json | cfssljson -bare client
```
