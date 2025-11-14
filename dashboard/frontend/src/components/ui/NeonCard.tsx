import React from 'react'
import { motion } from 'framer-motion'

interface NeonCardProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
  hoverable?: boolean
  glowColor?: 'cyan' | 'red' | 'purple' | 'none'
}

const GLOW_COLORS = {
  cyan: 'hover:border-neon-cyan/50 hover:shadow-neon-cyan',
  red: 'hover:border-neon-red/50 hover:shadow-neon-red',
  purple: 'hover:border-neon-purple/50 hover:shadow-neon-purple',
  none: '',
}

export const NeonCard: React.FC<NeonCardProps> = ({
  children,
  className = '',
  onClick,
  hoverable = true,
  glowColor = 'cyan',
}) => {
  const isClickable = !!onClick

  return (
    <motion.div
      onClick={onClick}
      className={`
        bg-bg-surface/80
        border
        border-neon-cyan/20
        rounded-xl
        p-6
        transition-all
        duration-300
        ${hoverable ? GLOW_COLORS[glowColor] : ''}
        ${isClickable ? 'cursor-pointer' : ''}
        ${className}
      `}
      whileHover={hoverable ? { y: -2, scale: 1.01 } : {}}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
