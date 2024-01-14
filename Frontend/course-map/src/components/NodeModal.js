import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const NodeModal = ({ showModal, handleClose, node }) => {
    const redirectToHandbook = () => {
      const newTab = window.open(node !== undefined ? node.data.url : 'https://google.com', '_blank');
      newTab.focus(); // Optional: Set focus on the new tab
    };
    return ( <div>{ node &&
      <Modal show={showModal} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{node.data.label}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p><strong>Course Title: </strong>{node.data.courseTitle}</p>
          <p>
            <strong>Offering Terms: </strong>
            {node.data.offeringTerms.length > 0 && node.data.offeringTerms}
            {node.data.offeringTerms.length <= 0 && 'Not being offered this year'}
          </p>
          {node.data.prereqs.length > 0 && <p><strong>Prerequisites: </strong>{node.data.prereqs}</p>}
          <p><strong>Field: </strong>{node.data.field}</p>
        </Modal.Body>
        <Modal.Footer>
            <Button variant="Primary" onClick={redirectToHandbook}>
                Handbook
            </Button>
            <Button variant="secondary" onClick={handleClose}>
                Close
            </Button>
        </Modal.Footer>
      </Modal>
    }</div> );
  };

  export default NodeModal;