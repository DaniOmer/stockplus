"""
Domain entities for the address application.
This module contains the domain entity for the address.
"""

from typing import Optional

class Address:
    """
    Entity for an address.
    """

    def __init__(
        self,
        address: Optional[str] = None,
        complement: Optional[str] = None,
        city: Optional[str] = None,
        postal_code: Optional[str] = None,
        state: Optional[str] = None,
        state_code: Optional[str] = None,
        country: Optional[str] = None,
        country_code: Optional[str] = None,
        cedex: Optional[str] = None,
        cedex_code: Optional[str] = None,
        special: Optional[str] = None,
        index: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ):
        self.address = address
        self.complement = complement
        self.city = city
        self.postal_code = postal_code
        self.state = state
        self.state_code = state_code
        self.country = country
        self.country_code = country_code
        self.cedex = cedex
        self.cedex_code = cedex_code
        self.special = special
        self.index = index
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"{self.address}, {self.city}, {self.postal_code}, {self.country}"

    def get_full_address(self) -> str:
        """
        Retourne l'adresse complète sous forme de chaîne de caractères.
        """
        parts = []

        if self.address:
            parts.append(self.address)

        if self.complement:
            parts.append(self.complement)

        city_parts = []
        if self.postal_code:
            city_parts.append(self.postal_code)

        if self.city:
            city_parts.append(self.city)

        if city_parts:
            parts.append(" ".join(city_parts))

        if self.state:
            parts.append(self.state)

        if self.country:
            parts.append(self.country)

        return ", ".join(parts)

    def get_coordinates(self) -> Optional[tuple]:
        """
        Retourne les coordonnées sous forme de tuple (latitude, longitude).
        """
        if self.latitude is not None and self.longitude is not None:
            return (self.latitude, self.longitude)
        return None
