import React, { useState } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import type { MetricsDataPoint } from '@/lib/types'
import { NeonCard } from '@/components/ui/NeonCard'
import { CHART_COLORS } from '@/lib/constants/colors'

interface QualityChartProps {
  data: MetricsDataPoint[]
}

export const QualityChart: React.FC<QualityChartProps> = ({ data }) => {
  const [activeLines, setActiveLines] = useState({
    system_quality: true,
    agent_8_quality: true,
    agent_5a_quality: true,
    agent_5b_quality: true,
  })

  const toggleLine = (key: keyof typeof activeLines) => {
    setActiveLines((prev) => ({ ...prev, [key]: !prev[key] }))
  }

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp)
    return `${date.getMonth() + 1}/${date.getDate()}`
  }

  return (
    <NeonCard hoverable={false}>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-text-primary">
            Quality Metrics (7 Days)
          </h2>
        </div>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 240, 255, 0.1)" />
            <XAxis
              dataKey="timestamp"
              tickFormatter={formatDate}
              stroke="#a0aff0"
              style={{ fontSize: 12 }}
            />
            <YAxis
              domain={[0, 10]}
              stroke="#a0aff0"
              style={{ fontSize: 12 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1a1f3a',
                border: '1px solid #00f0ff',
                borderRadius: '8px',
                color: '#e0e8ff',
              }}
              labelStyle={{ color: '#00f0ff' }}
            />
            <Legend
              onClick={(e) => {
                const key = e.dataKey as keyof typeof activeLines
                toggleLine(key)
              }}
              wrapperStyle={{ cursor: 'pointer' }}
            />

            {activeLines.system_quality && (
              <Line
                type="monotone"
                dataKey="system_quality"
                stroke={CHART_COLORS.SYSTEM_QUALITY}
                strokeWidth={3}
                dot={{ fill: CHART_COLORS.SYSTEM_QUALITY, r: 4 }}
                activeDot={{ r: 6 }}
                name="System Quality"
              />
            )}

            {activeLines.agent_8_quality && (
              <Line
                type="monotone"
                dataKey="agent_8_quality"
                stroke={CHART_COLORS.AGENT_8}
                strokeWidth={2}
                dot={{ fill: CHART_COLORS.AGENT_8, r: 3 }}
                name="Agent 8"
              />
            )}

            {activeLines.agent_5a_quality && (
              <Line
                type="monotone"
                dataKey="agent_5a_quality"
                stroke={CHART_COLORS.AGENT_5A}
                strokeWidth={2}
                dot={{ fill: CHART_COLORS.AGENT_5A, r: 3 }}
                name="Agent 5a"
              />
            )}

            {activeLines.agent_5b_quality && (
              <Line
                type="monotone"
                dataKey="agent_5b_quality"
                stroke={CHART_COLORS.AGENT_5B}
                strokeWidth={2}
                dot={{ fill: CHART_COLORS.AGENT_5B, r: 3 }}
                name="Agent 5b"
              />
            )}
          </LineChart>
        </ResponsiveContainer>

        <div className="text-xs text-text-secondary text-center">
          Click on legend items to toggle visibility
        </div>
      </div>
    </NeonCard>
  )
}
