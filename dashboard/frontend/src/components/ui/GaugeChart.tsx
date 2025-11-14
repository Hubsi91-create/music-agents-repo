import React from 'react'
import { COLORS } from '@/lib/constants/colors'

interface GaugeChartProps {
  value: number // 0-100
  label: string
  color?: string
}

export const GaugeChart: React.FC<GaugeChartProps> = ({ value, label, color }) => {
  // Determine color based on value if not provided
  const getColor = () => {
    if (color) return color
    if (value < 50) return COLORS.SUCCESS
    if (value < 75) return COLORS.WARNING
    return COLORS.ERROR
  }

  const gaugeColor = getColor()
  const percentage = Math.min(Math.max(value, 0), 100)

  // SVG semicircle parameters
  const size = 200
  const strokeWidth = 20
  const radius = (size - strokeWidth) / 2
  const circumference = Math.PI * radius // Half circle
  const offset = circumference - (percentage / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size / 2 + 20 }}>
        <svg
          width={size}
          height={size / 2 + 20}
          className="overflow-visible"
        >
          {/* Background arc */}
          <path
            d={`M ${strokeWidth / 2} ${size / 2} A ${radius} ${radius} 0 0 1 ${size - strokeWidth / 2} ${size / 2}`}
            fill="none"
            stroke="rgba(0, 240, 255, 0.1)"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />
          {/* Progress arc */}
          <path
            d={`M ${strokeWidth / 2} ${size / 2} A ${radius} ${radius} 0 0 1 ${size - strokeWidth / 2} ${size / 2}`}
            fill="none"
            stroke={gaugeColor}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-700 ease-out"
            style={{
              filter: `drop-shadow(0 0 8px ${gaugeColor})`,
            }}
          />
        </svg>

        {/* Value display */}
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 text-center">
          <div
            className="text-3xl font-bold"
            style={{ color: gaugeColor }}
          >
            {Math.round(percentage)}%
          </div>
        </div>
      </div>

      {/* Label */}
      <div className="text-sm text-text-secondary uppercase tracking-wider">
        {label}
      </div>
    </div>
  )
}
