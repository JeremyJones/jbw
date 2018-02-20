from requests import get as url_get
from json import loads as jsonloads
from behaviours.variance import \
     set_variance_behaviour as default_variance_behaviour
from behaviours.natural_log import \
     set_natural_log_behaviour as default_natural_log_behaviour


class Feed:
    classification = 'quandl.v3.WIKI'

    def __init__(self, symbol: str, url: str=None, data=None,
                 shelf=None, mongodb=None,
                 variance_behaviour=None,
                 natural_log_behaviour=None) -> None:
        self.symbol = symbol
        self.url = url
        self.data = data

        try:
            if type(self.data) is str:   # could be a dict already, or None
                self.data = jsonloads(self.data)
        except TypeError:
            pass

        if shelf is not None:
            self.restore(shelf)

        self._variance_behaviour = (variance_behaviour or
                                    default_variance_behaviour)

        self.variance_behaviour = self._variance_behaviour()

        self._natural_log_behaviour = (natural_log_behaviour or
                                       default_natural_log_behaviour)

        self.natural_log_behaviour = self._natural_log_behaviour()

    def __repr__(self) -> str:
        return 'Feed("{s}", "{u}", {d})'.format(
            s=self.symbol,
            u=self.url,
            d='"{}"'.format(self.data) if self.data else "None"
        )

    def restore(self, shelf=None) -> None:
        self.data = shelf.get(self.symbol)

    def _refresh_feed(self) -> None:
        self.data = url_get(self.url).json()

    def refresh(self) -> bool:
        try:
            with Timeout(seconds=10):
                self._refresh_feed()
        except TimeoutError:
            self.data = None
            return False
        else:
            return True

    def add_variance(self) -> None:
        """
        Add variance information to the whole dataset.
        """
        self.variance_behaviour.set_variance(self)

    def add_natural_log(self) -> None:
        """
        Add Natural Log numbers to the whole dataset.
        """
        self.natural_log_behaviour.set_natural_log(self)
