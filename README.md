# pkcs11-python-sign

example to illustrate pkcs#11 sign using python (tested only with NitroKey HSM)


## prerequiste 

```
sudo pip3 install python-pkcs11 pycryptodome
```


## create Keys

```
$ export PKCS11_MODULE=/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
$ pkcs11-tool --list-slots --module $PKCS11_MODULE 
$ pkcs11-tool --keypairgen --key-type EC:prime256v1 --label "testkeyEC666" --id 666  -l --pin 123456 --usage-sign --module $PKCS11_MODULE
```

