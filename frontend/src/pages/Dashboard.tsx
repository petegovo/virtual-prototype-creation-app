import React from 'react'
import { Link } from 'react-router-dom'
import { 
  Package, 
  Layers, 
  Workflow, 
  Play, 
  Upload,
  BarChart3,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react'

export default function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">
          Welcome to Virtual Prototype Creation
        </h1>
        <p className="text-primary-100 text-lg">
          Integrate SystemC, Simulink, and Modelica IP using FMI 3.0 and SSP 2.0 standards
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="card-content p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total FMUs</p>
                <p className="text-2xl font-bold text-gray-900">12</p>
              </div>
              <Package className="w-8 h-8 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-content p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">SSP Packages</p>
                <p className="text-2xl font-bold text-gray-900">5</p>
              </div>
              <Layers className="w-8 h-8 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-content p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Projects</p>
                <p className="text-2xl font-bold text-gray-900">3</p>
              </div>
              <Workflow className="w-8 h-8 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-content p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Simulations</p>
                <p className="text-2xl font-bold text-gray-900">28</p>
              </div>
              <BarChart3 className="w-8 h-8 text-primary-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Link to="/fmu" className="card hover:shadow-md transition-shadow">
          <div className="card-content p-6">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-blue-100 rounded-lg">
                <Upload className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Upload FMU</h3>
                <p className="text-sm text-gray-600">Import SystemC, Simulink, or Modelica models</p>
              </div>
            </div>
          </div>
        </Link>

        <Link to="/designer" className="card hover:shadow-md transition-shadow">
          <div className="card-content p-6">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <Workflow className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Design System</h3>
                <p className="text-sm text-gray-600">Create virtual prototype architectures</p>
              </div>
            </div>
          </div>
        </Link>

        <Link to="/simulation" className="card hover:shadow-md transition-shadow">
          <div className="card-content p-6">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-purple-100 rounded-lg">
                <Play className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Run Simulation</h3>
                <p className="text-sm text-gray-600">Execute co-simulation scenarios</p>
              </div>
            </div>
          </div>
        </Link>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">Recent FMUs</h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Package className="w-5 h-5 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">SystemC_Motor_Controller.fmu</p>
                    <p className="text-sm text-gray-600">FMI 3.0 • Co-Simulation</p>
                  </div>
                </div>
                <CheckCircle className="w-5 h-5 text-green-500" />
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Package className="w-5 h-5 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">Simulink_Battery_Model.fmu</p>
                    <p className="text-sm text-gray-600">FMI 3.0 • Model Exchange</p>
                  </div>
                </div>
                <CheckCircle className="w-5 h-5 text-green-500" />
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Package className="w-5 h-5 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">Modelica_Thermal_System.fmu</p>
                    <p className="text-sm text-gray-600">FMI 3.0 • Scheduled Execution</p>
                  </div>
                </div>
                <AlertCircle className="w-5 h-5 text-yellow-500" />
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">System Status</h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                  <span className="text-gray-900">FMI 3.0 Support</span>
                </div>
                <span className="text-sm text-green-600 font-medium">Active</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                  <span className="text-gray-900">SSP 2.0 Support</span>
                </div>
                <span className="text-sm text-green-600 font-medium">Active</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                  <span className="text-gray-900">Simulation Engine</span>
                </div>
                <span className="text-sm text-green-600 font-medium">Ready</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-blue-400 rounded-full"></div>
                  <span className="text-gray-900">WebSocket Connection</span>
                </div>
                <span className="text-sm text-blue-600 font-medium">Connected</span>
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <Clock className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-900">
                  Last system check: 2 minutes ago
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Highlights */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold">Platform Features</h3>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Package className="w-6 h-6 text-primary-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">FMI 3.0 Compliance</h4>
              <p className="text-sm text-gray-600">
                Full support for the latest FMI standard including arrays, clocks, and scheduled execution
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Layers className="w-6 h-6 text-green-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">SSP 2.0 Integration</h4>
              <p className="text-sm text-gray-600">
                Advanced system structure and parameterization with architectural exchange capabilities
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Workflow className="w-6 h-6 text-purple-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Multi-Domain Co-Simulation</h4>
              <p className="text-sm text-gray-600">
                Seamless integration of SystemC, Simulink, and Modelica models in unified simulations
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}