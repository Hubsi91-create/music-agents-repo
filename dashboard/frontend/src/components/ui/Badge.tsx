import React from 'react'
import type { BadgeVariant } from '@/lib/types'

interface BadgeProps {
  children: React.ReactNode
  variant?: BadgeVariant
  className?: string
  icon?: React.ReactNode
}

const VARIANT_STYLES: Record<BadgeVariant, string> = {
  success: 'bg-neon-green/20 text-neon-green border-neon-green/50',
  warning: 'bg-neon-yellow/20 text-neon-yellow border-neon-yellow/50',
  error: 'bg-neon-red/20 text-neon-red border-neon-red/50',
  info: 'bg-neon-cyan/20 text-neon-cyan border-neon-cyan/50',
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'info',
  className = '',
  icon,
}) => {
  return (
    <span
      className={`
        inline-flex
        items-center
        gap-1.5
        px-3
        py-1
        rounded-full
        text-xs
        font-semibold
        uppercase
        tracking-wide
        border
        ${VARIANT_STYLES[variant]}
        ${className}
      `}
    >
      {icon && <span className="text-sm">{icon}</span>}
      {children}
    </span>
  )
}
