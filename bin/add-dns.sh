#!/bin/bash

set -e

DOMAIN=${DOMAIN:=cloudet.xyz}

USAGE='Usage: `basename $0` --hostname HOSTNAME [--domain DOMAIN]'

# Parse args
while [[ $# > 0 ]]
do
key="$1"
case $key in
    -H|--hostname)
    HOST="$2"
    shift # past argument
    ;;
    -D|--domain)
    DOMAIN="$2"
    shift # past argument
    ;;
    *) # other option
    ;;
esac
shift # past argument or value
done

if [ -z "${HOST:+x}" ]; then
	 echo "ERROR: Must provide --hostname option"; exit 1;
fi

# Lookup ID by hostname
PRIMARY_IP=$(slcli --format raw virtual list \
  --hostname "$HOST" --domain "$DOMAIN" \
  --columns primary_ip --sortby primary_ip)

# Get device details
slcli dns record-add $DOMAIN $HOST A $PRIMARY_IP
