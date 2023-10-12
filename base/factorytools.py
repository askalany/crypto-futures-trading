from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def run(self):
        pass


class StrategyCreator(ABC):
    @abstractmethod
    def create(self) -> Strategy:
        pass

    def run(self):
        self.create().run()


class FRStrategy(Strategy):
    def run(self):
        pass


class PMAQStrategy(Strategy):
    def run(self):
        pass


class FRStrategyCreator(StrategyCreator):
    def create(self) -> Strategy:
        return FRStrategy()


class PMAQStrategyCreator(StrategyCreator):
    def create(self) -> Strategy:
        return PMAQStrategy()


class StrategyCreatorFactory:
    def create_fr_strategy(self) -> StrategyCreator:
        return FRStrategyCreator()

    def create_pmaq_strategy(self) -> StrategyCreator:
        return PMAQStrategyCreator()


def main() -> None:
    factory = StrategyCreatorFactory()
    factory.create_fr_strategy().run()
    factory.create_pmaq_strategy().run()
    fr_trading_strategy_creator = FRStrategyCreator()
    fr_trading_strategy_creator.run()
    pmaq_trading_strategy_creator = PMAQStrategyCreator()
    pmaq_trading_strategy_creator.run()


if __name__ == "__main__":
    main()
