'use client'

import React from 'react'

interface NeonButtonProps {
  children: React.ReactNode
  variant?: 'cyan' | 'red' | 'purple' | 'green'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  className?: string
}

export default function NeonButton({
  children,
  variant = 'cyan',
  size = 'md',
  onClick,
  disabled = false,
  type = 'button',
  className = '',
}: NeonButtonProps) {
  const variantClasses = {
    cyan: 'btn-neon-cyan',
    red: 'btn-neon-red',
    purple: 'btn-neon-purple',
    green: 'border-success-green text-success-green shadow-[0_0_10px_#00e676]',
  }

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-8 py-3 text-base',
    lg: 'px-12 py-4 text-lg',
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`btn-neon ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
    >
      {children}
    </button>
  )
}
