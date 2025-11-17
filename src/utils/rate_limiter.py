"""Rate limiter per controllare la frequenza delle richieste."""

import time
import random
from threading import Lock
from typing import Optional
import logging


logger = logging.getLogger(__name__)


class RateLimiter:
    """Gestisce il rate limiting delle richieste HTTP."""

    def __init__(
        self,
        requests_per_second: float = 0.5,
        min_delay: float = 2.0,
        max_delay: float = 5.0
    ):
        """
        Inizializza il rate limiter.

        Args:
            requests_per_second: Numero massimo di richieste al secondo
            min_delay: Delay minimo tra richieste (secondi)
            max_delay: Delay massimo tra richieste (secondi)
        """
        self.requests_per_second = requests_per_second
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time: Optional[float] = None
        self._lock = Lock()

        # Calcola il delay basato su requests_per_second
        self.base_delay = 1.0 / requests_per_second if requests_per_second > 0 else min_delay

        logger.info(
            f"RateLimiter inizializzato: {requests_per_second} req/s, "
            f"delay: {min_delay}-{max_delay}s"
        )

    def wait(self) -> float:
        """
        Attende il tempo necessario prima della prossima richiesta.

        Returns:
            Il tempo atteso in secondi
        """
        with self._lock:
            current_time = time.time()

            if self.last_request_time is not None:
                # Calcola quanto tempo è passato dall'ultima richiesta
                elapsed = current_time - self.last_request_time

                # Calcola delay casuale tra min e max
                delay = random.uniform(self.min_delay, self.max_delay)

                # Assicurati di rispettare anche il base_delay
                required_delay = max(delay, self.base_delay)

                # Se non è passato abbastanza tempo, aspetta
                if elapsed < required_delay:
                    sleep_time = required_delay - elapsed
                    logger.debug(f"Rate limiting: attendo {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                    actual_wait = sleep_time
                else:
                    actual_wait = 0.0
            else:
                actual_wait = 0.0

            # Aggiorna il timestamp dell'ultima richiesta
            self.last_request_time = time.time()

            return actual_wait

    def reset(self):
        """Resetta il rate limiter."""
        with self._lock:
            self.last_request_time = None
            logger.debug("RateLimiter resettato")

    def __enter__(self):
        """Context manager entry."""
        self.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass
