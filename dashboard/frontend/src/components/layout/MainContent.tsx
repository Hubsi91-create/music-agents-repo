import React from 'react'
import styles from '@/styles/layout.module.css'

interface MainContentProps {
  children: React.ReactNode
}

export const MainContent: React.FC<MainContentProps> = ({ children }) => {
  return (
    <main className={styles.mainContent}>
      <div className="p-8">{children}</div>
    </main>
  )
}
