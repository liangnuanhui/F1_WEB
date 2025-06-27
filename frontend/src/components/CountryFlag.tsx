"use client";

import { getCountryCode } from "@/lib/utils";

interface CountryFlagProps {
  country: string;
  className?: string;
}

export function CountryFlag({ country, className }: CountryFlagProps) {
  const countryCode = getCountryCode(country);

  if (!countryCode) {
    return null; // Or a placeholder
  }

  return (
    <img
      src={`/country_flags/${countryCode}.svg`}
      alt={`${country} flag`}
      className={className || "w-6 h-auto"}
      title={country}
    />
  );
}
