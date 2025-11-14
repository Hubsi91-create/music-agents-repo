import React, { useEffect, useState } from 'react'
import { Storyboard } from '@/components/storyboard/Storyboard'
import { getStoryboardProjects } from '@/lib/api/client'
import type { StoryboardProject } from '@/lib/types'

export const StoryboardPage: React.FC = () => {
  const [project, setProject] = useState<StoryboardProject | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadProjects = async () => {
      try {
        const projects = await getStoryboardProjects()
        // Load the first project if available
        if (projects.length > 0) {
          setProject(projects[0])
        }
      } catch (error) {
        console.error('Failed to load storyboard projects:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadProjects()
  }, [])

  const handleExport = () => {
    console.log('Export storyboard')
    // TODO: Implement export functionality
  }

  const handleShare = () => {
    console.log('Share storyboard')
    // TODO: Implement share functionality
  }

  const handleAddScene = () => {
    console.log('Add scene')
    // TODO: Implement add scene functionality
  }

  const handleEditScene = (scene: any) => {
    console.log('Edit scene:', scene)
    // TODO: Implement edit scene functionality
  }

  const handleDeleteScene = (sceneId: string) => {
    console.log('Delete scene:', sceneId)
    // TODO: Implement delete scene functionality
  }

  return (
    <Storyboard
      project={project}
      isLoading={isLoading}
      onExport={handleExport}
      onShare={handleShare}
      onAddScene={handleAddScene}
      onEditScene={handleEditScene}
      onDeleteScene={handleDeleteScene}
    />
  )
}
