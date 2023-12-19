#! /usr/bin/env bash
set -euxo nounset -o pipefail
exec 0>&-

if (( ! UID )) ; then
echo Run as non-root 1>&2
exit 1
fi

if (( $# )) ; then
cat 1>&2 << EOF
Usage: $0
(expects no parameters)
EOF
exit 1
fi

if command -v shellcheck ; then
	shellcheck "$0"
fi

echo "pulling latest version"
git pull

if [[ ! -d venv ]] ; then
  echo "creating virtual environment"
  python -m venv venv
fi

echo "activating virtual environment"
# shellcheck disable=SC1091
source venv/bin/activate

[[ -e .env ]]
# shellcheck disable=SC1091
. .env
[[ "$DISCORD_TOKEN" ]]
[[ "$DISCORD_GUILD" ]]
[[ "$DISCORD_CHANNEL" ]]
[[ "$SUPABASE_KEY"  ]]
[[ "$INVITE_TRACKER_ID" ]]
export DISCORD_TOKEN
export DISCORD_GUILD
export DISCORD_CHANNEL
export SUPABASE_KEY
export INVITE_TRACKER_ID

echo "installing discord bot module"
pip install .

echo "running main.py"
python -m message_tracker_bot

echo "saving changes to git"
git add .
git commit -m "[$0]: updates"
git push
