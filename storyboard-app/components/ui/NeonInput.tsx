'use client'

import React from 'react'

interface NeonInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  type?: 'text' | 'password' | 'email'
  disabled?: boolean
  className?: string
}

export default function NeonInput({
  value,
  onChange,
  placeholder,
  type = 'text',
  disabled = false,
  className = '',
}: NeonInputProps) {
  return (
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      disabled={disabled}
      className={`input-neon w-full ${className}`}
    />
  )
}
