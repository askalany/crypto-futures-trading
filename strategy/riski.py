from repository.repository import TradeRepo


def get_margin_ratio():
    repo = TradeRepo()
    account_info = repo.get_account_info()
    maintenance_margin = account_info.totalMaintMargin
    total_wallet_balance = account_info.totalWalletBalance
    return maintenance_margin / total_wallet_balance