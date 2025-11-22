import React from 'react'
import { User, Phone, CreditCard, Package, FileText } from 'lucide-react'

function OrderDisplay({ orderData }) {
  if (!orderData) return null

  const formatCurrency = (amount) => {
    return `${amount.toFixed(3)} BD`
  }

  return (
    <div className="space-y-4">
      {/* Order ID */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-1">
          <FileText className="w-4 h-4 text-indigo-600" />
          <span className="text-xs font-medium text-indigo-600">Order ID</span>
        </div>
        <p className="text-lg font-bold text-gray-800">{orderData.order_id}</p>
      </div>

      {/* Customer Info */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-3">
          <User className="w-4 h-4 text-gray-600" />
          <span className="text-sm font-semibold text-gray-700">Customer</span>
        </div>
        <div className="space-y-2 text-sm">
          <p><span className="text-gray-600">Name:</span> <span className="font-medium">{orderData.customer?.name || 'N/A'}</span></p>
          <p><span className="text-gray-600">CPR:</span> <span className="font-medium">{orderData.customer?.cpr || 'N/A'}</span></p>
          <p><span className="text-gray-600">Mobile:</span> <span className="font-medium">{orderData.customer?.mobile || 'N/A'}</span></p>
        </div>
      </div>

      {/* Order Type */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-2">
          <Package className="w-4 h-4 text-gray-600" />
          <span className="text-sm font-semibold text-gray-700">Order Type</span>
        </div>
        <p className="text-sm font-medium text-gray-800 capitalize">
          {orderData.order_type?.replace('_', ' ') || 'N/A'}
        </p>
        {orderData.line_details && (
          <div className="mt-2 text-xs text-gray-600">
            {orderData.line_details.type && (
              <p>Type: <span className="font-medium capitalize">{orderData.line_details.type}</span></p>
            )}
            {orderData.line_details.number && (
              <p>Number: <span className="font-medium">{orderData.line_details.number}</span></p>
            )}
            {orderData.line_details.sub_number && (
              <p>Sub Number: <span className="font-medium">{orderData.line_details.sub_number}</span></p>
            )}
          </div>
        )}
      </div>

      {/* Device */}
      {orderData.device && (
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Package className="w-4 h-4 text-gray-600" />
            <span className="text-sm font-semibold text-gray-700">Device</span>
          </div>
          <p className="text-sm font-medium text-gray-800">{orderData.device.name || 'N/A'}</p>
          {(orderData.device.variant || orderData.device.color) && (
            <p className="text-xs text-gray-600 mt-1">
              {orderData.device.variant} {orderData.device.color}
            </p>
          )}
        </div>
      )}

      {/* Plan */}
      {orderData.plan && (
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <CreditCard className="w-4 h-4 text-gray-600" />
            <span className="text-sm font-semibold text-gray-700">Plan</span>
          </div>
          <p className="text-sm font-medium text-gray-800">{orderData.plan.name || 'N/A'}</p>
          {orderData.plan.selected_commitment && (
            <p className="text-xs text-gray-600 mt-1">
              {orderData.plan.selected_commitment} months commitment
            </p>
          )}
        </div>
      )}

      {/* Financial */}
      {orderData.financial && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-3">
            <CreditCard className="w-4 h-4 text-green-600" />
            <span className="text-sm font-semibold text-green-700">Financial Details</span>
          </div>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Monthly:</span>
              <span className="font-medium">{formatCurrency(orderData.financial.monthly || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Advance:</span>
              <span className="font-medium">{formatCurrency(orderData.financial.advance || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Upfront:</span>
              <span className="font-medium">{formatCurrency(orderData.financial.upfront || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">VAT:</span>
              <span className="font-medium">{formatCurrency(orderData.financial.vat || 0)}</span>
            </div>
            <div className="flex justify-between pt-2 border-t border-green-200">
              <span className="font-semibold text-green-700">Total:</span>
              <span className="font-bold text-green-700">{formatCurrency(orderData.financial.total || 0)}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default OrderDisplay

