# Q1
## TL;DR

Using `ProxyJump`

```
ssh -J your.bastion.host remote.internal.host
```

## Extensive

If no VPN can be used, jumping over bastion host to remote server can be achieved using `ssh`'s ProxyJump option (`man ssh | less +/-J`). Bastion host should also be secured to prevent all other actions than ProxyJump. [Example](https://askubuntu.com/questions/48129/how-to-create-a-restricted-ssh-user-for-port-forwarding) `sshd` configuration. Intrusion prevention like file2ban is also a good idea since ssh port most probably is opened publicly.

# Q2
## TL;DR

Requirements:

* `python3`
* `pyyaml`
* `argparse`
* `openssh>=7.3`

```
python3 ssh-conf-gen.py -i inventory.yaml -o config-additional
```

```
echo "Include $(pwd)/config-additional" >> ssh-conf-mockup
```

```
ssh serverN
```

## Extensive

The most native and simple way of connecting to multiple servers that comes to my mind is by defining those hosts in `~/.ssh/config` and simply connecting by `ssh serverN`. In order to keep things tidy and allowing to regenerate file without risk of loosing main `config` file `Include` was used. It points to separate file with generated hosts. Since config file is rendered by shell when `ssh [TAB]` it's possible in theory, that file with too many entries will slow down shell. Since it's hard to tell *how many* are *too many* and this approach is fairly simple I'd recommend giving it a try before overcomplicating things. As a bonus, `scp` will also work.

Above code can be run if `python3` (or `python2` after adjustments) is available. If not, generating ssh config file using `docker` (described below) is also possible. Script by default uses `~/ssh/id_ed25519` as default `IdentityFile`, but that can be overwritten using `-k` parameter. Other options can be easily parametrised or hardcoded (like `User ubuntu`) directly in the script.

`ssh-conf-mockup` used in examples should be replaced with `~/.ssh/config` in real life.

`python3 ssh-conf-gen.py -h` prints out short help.

### Docker
Requirements:

* `docker`
* `openssh>=7.3`

```
docker image build -t ssh-conf-gen .
```

```
INPUT='inventory.yaml' \
OUTPUT='config-additional'; \
touch ${OUTPUT}; \
docker run \
  -v $(pwd)/${INPUT}:/${INPUT} \
  -v $(pwd)/${OUTPUT}:/${OUTPUT} \
  -t ssh-conf-gen \
  python3 ssh-conf-gen.py -i ${INPUT} -o ${OUTPUT} &&\
echo "Include $(pwd)/${OUTPUT}" >> ssh-conf-mockup
```
