import React from 'react';

export default function ConfirmDialog({ title, message, name, onConfirm, onCancel }) {
  return (
    <div className="overlay" onClick={onCancel}>
      <div className="modal" style={{ width: 380 }} onClick={e => e.stopPropagation()}>
        <div className="confirm-icon">⚠️</div>
        <div className="modal-title" style={{ textAlign: 'center' }}>{title}</div>
        <p className="confirm-msg">
          {message} <span className="confirm-name">{name}</span>?<br />
          This action cannot be undone.
        </p>
        <div className="modal-actions" style={{ justifyContent: 'center' }}>
          <button className="btn btn-ghost" onClick={onCancel}>Cancel</button>
          <button className="btn btn-danger" style={{ padding: '8px 20px' }} onClick={onConfirm}>
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
