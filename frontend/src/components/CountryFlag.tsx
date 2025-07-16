"use client";

import Image from "next/image";
import ReactCountryFlag from "react-country-flag";
import { countryCodeMap } from "@/lib/country-code-map";
import { nationalityToFlagCode } from "@/lib/nationality-to-flag-code";

export function CountryFlag({
  country,
  nationality,
  className = "",
  size = "1.5em", // 默认尺寸
  ...props
}: {
  country?: string;
  nationality?: string;
  className?: string;
  size?: string;
  [key: string]: unknown;
}) {
  // 方案一：根据国籍，使用 react-country-flag 库 (统一方式)
  if (nationality) {
    const countryCode = nationalityToFlagCode[nationality];
    if (!countryCode) return null;

    return (
      <ReactCountryFlag
        countryCode={countryCode}
        svg
        style={{
          fontSize: size, // 通过fontSize控制表情符号国旗的大小
          lineHeight: "1",
        }}
        className={`inline-block ${className}`}
        title={nationality}
        {...props}
      />
    );
  }

  // 方案二：根据国家/地点，使用本地的 SVG 文件 (兼容旧代码)
  if (country) {
    const countryCode = countryCodeMap[country];

    // 添加调试信息（仅在开发环境）
    if (process.env.NODE_ENV === "development") {
      console.log(
        `CountryFlag: country="${country}" -> countryCode="${countryCode}"`
      );
    }

    if (!countryCode) {
      console.warn(`No country code found for "${country}"`);
      return null;
    }

    const flagPath = `/country_flags/${countryCode.toUpperCase()}.svg`;

    return (
      <Image
        src={flagPath}
        alt={`${country} flag`}
        title={country}
        width={20}
        height={15}
        className={className}
        onError={() => {
          console.error(
            `Failed to load flag image: ${flagPath} for country: ${country}`
          );
        }}
        {...props}
      />
    );
  }

  return null;
}
