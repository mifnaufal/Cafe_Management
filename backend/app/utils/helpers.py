from datetime import datetime, timezone


def generate_transaction_number() -> str:
    now = datetime.now(timezone.utc)
    date_part = now.strftime("%Y%m%d")
    return f"TRX-{date_part}-{now.strftime('%f')[:3]}"
