import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  Home, 
  Package, 
  Layers, 
  Workflow, 
  Play, 
  FolderOpen,
  Settings,
  HelpCircle
} from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'FMU Manager', href: '/fmu', icon: Package },
  { name: 'SSP Manager', href: '/ssp', icon: Layers },
  { name: 'System Designer', href: '/designer', icon: Workflow },
  { name: 'Simulation', href: '/simulation', icon: Play },
  { name: 'Projects', href: '/projects', icon: FolderOpen },
]

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="flex flex-col w-64 bg-white shadow-lg">
        {/* Logo */}
        <div className="flex items-center justify-center h-16 px-4 bg-primary-600">
          <h1 className="text-xl font-bold text-white">
            Virtual Prototype
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            const Icon = item.icon
            
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`
                  flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors
                  ${isActive 
                    ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-600' 
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }
                `}
              >
                <Icon className="w-5 h-5 mr-3" />
                {item.name}
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="px-4 py-4 border-t border-gray-200">
          <div className="flex items-center space-x-3">
            <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
              <Settings className="w-5 h-5" />
            </button>
            <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
              <HelpCircle className="w-5 h-5" />
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            FMI 3.0 • SSP 2.0
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900">
                  {navigation.find(item => item.href === location.pathname)?.name || 'Virtual Prototype'}
                </h2>
                <p className="text-sm text-gray-600 mt-1">
                  SystemC • Simulink • Modelica Integration Platform
                </p>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>System Ready</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto">
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}