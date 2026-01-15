import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Prevent the warning about multiple lockfiles
  experimental: {
    serverHooks: true,
  },
};

export default nextConfig;
