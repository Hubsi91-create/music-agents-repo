import React from 'react'
import { motion } from 'framer-motion'
import type { NeonColor, ButtonSize } from '@/lib/types'

interface NeonButtonProps {
  children: React.ReactNode
  variant?: NeonColor
  size?: ButtonSize
  onClick?: () => void
  loading?: boolean
  disabled?: boolean
  icon?: React.ReactNode
  className?: string
  type?: 'button' | 'submit' | 'reset'
}

const VARIANT_STYLES: Record<NeonColor, string> = {
  cyan: 'border-neon-cyan text-neon-cyan hover:bg-neon-cyan/10 hover:shadow-neon-cyan',
  red: 'border-neon-red text-neon-red hover:bg-neon-red/10 hover:shadow-neon-red',
  purple: 'border-neon-purple text-neon-purple hover:bg-neon-purple/10 hover:shadow-neon-purple',
  green: 'border-neon-green text-neon-green hover:bg-neon-green/10 hover:shadow-neon-green',
  yellow: 'border-neon-yellow text-neon-yellow hover:bg-neon-yellow/10 hover:shadow-neon-yellow',
}

const SIZE_STYLES: Record<ButtonSize, string> = {
  sm: 'px-4 py-2 text-xs',
  md: 'px-8 py-3 text-sm',
  lg: 'px-12 py-4 text-base',
}

export const NeonButton: React.FC<NeonButtonProps> = ({
  children,
  variant = 'cyan',
  size = 'md',
  onClick,
  loading = false,
  disabled = false,
  icon,
  className = '',
  type = 'button',
}) => {
  const isDisabled = disabled || loading

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={isDisabled}
      className={`
        relative
        inline-flex
        items-center
        justify-center
        gap-2
        border-2
        rounded-full
        font-semibold
        uppercase
        tracking-wider
        transition-all
        duration-300
        ${VARIANT_STYLES[variant]}
        ${SIZE_STYLES[size]}
        ${isDisabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        ${className}
      `}
      whileHover={!isDisabled ? { scale: 1.05 } : {}}
      whileTap={!isDisabled ? { scale: 0.98 } : {}}
    >
      {loading && (
        <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
      )}
      {!loading && icon && <span>{icon}</span>}
      <span>{children}</span>
    </motion.button>
  )
}
