# pagerduty_autoack

Check for and automatically acknowledge/resolve PagerDuty incidents

## Example Usage

Bash:

```bash
export API_KEY="abc123"
export REGEX="Regex search value"
export QUERYINTERVAL="200"

pip install -r src/requirements.txt
python src/pagerduty_autoack.py
```

Docker:

```bash
docker build -t pagerduty_autoack .
docker run -d --name "py-pagerduty-autoack" -e API_KEY="abc123" -e REGEX="Regex search value" -e QUERYINTERVAL="200" --init pagerduty_autoack
```
