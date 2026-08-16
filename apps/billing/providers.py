from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CheckoutSession:
    id: str
    url: str


class BillingProvider(ABC):
    @abstractmethod
    def create_checkout(
        self,
        *,
        customer_reference: str,
        plan_id: str,
    ) -> CheckoutSession:
        raise NotImplementedError

    @abstractmethod
    def create_customer(
        self,
        *,
        email: str,
        name: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_payment(self, payment_id: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def refund(self, payment_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def process_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> dict:
        raise NotImplementedError


class NullBillingProvider(BillingProvider):
    def create_checkout(
        self,
        *,
        customer_reference: str,
        plan_id: str,
    ) -> CheckoutSession:
        raise RuntimeError("Billing is disabled.")

    def create_customer(
        self,
        *,
        email: str,
        name: str,
    ) -> str:
        raise RuntimeError("Billing is disabled.")

    def get_payment(self, payment_id: str) -> dict:
        raise RuntimeError("Billing is disabled.")

    def refund(self, payment_id: str) -> None:
        raise RuntimeError("Billing is disabled.")

    def process_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> dict:
        raise RuntimeError("Billing is disabled.")
