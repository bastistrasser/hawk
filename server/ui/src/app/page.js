'use client'

import { useState } from 'react';
import ColumnInfo from './column_info/page';
import WorkflowOverview from './workflow_overview/page'
import RunSelection from './run_selection/page';
import { Container, Row, Button } from 'react-bootstrap';
import { fetchRun } from './api-client';
import { MarkerType } from "reactflow";

export default function Home() {
  const [datasets, setDatasets] = useState([]);
  const [processingSteps, setProcessingSteps] = useState([]);
  const [runId, setRunId] = useState('');
  const [selectedDatasets, setSelectedDatasets] = useState([]);
  const [selectedProcessingSteps, setSelectedProcessingSteps] = useState([]);

  const handleClick = () => {
    fetchRun(runId)
      .then(run => {
        setDatasets([]);
        setProcessingSteps([]);
        run['processing_steps'].forEach(step => {
          const node = {
            id: step['description'],
            selectable: true,
            data: { label: String(datasetId) },
            position: { x: 0, y: 0 }
          }
          setDatasets(oldDatasets => [...oldDatasets, node]);
        });
        run['processing_steps'].forEach(step => {
          const edge = {
            source: String(step['input']),
            target: String(step['output']),
            label: step['description'],
            markerEnd: {
              type: MarkerType.Arrow
            }
          }
          setProcessingSteps(oldProcessingSteps => [...oldProcessingSteps, edge]);
        });
      });
  };

  return (
    <Container>
      <Row>
        <RunSelection key='runSelection' setRunId={setRunId} />        
      </Row>
      <Row className='mt-3'>
        <Button onClick={handleClick}>Show Pipeline</Button>
      </Row>
      <Row className='mt-3'>
        {datasets.length > 0 && processingSteps.length > 0
          ? <WorkflowOverview 
              key='workflowOverview'
              datasets={datasets}
              processingSteps={processingSteps}
              setSelectedDatasets={setSelectedDatasets}
              setSelectedProcessingSteps={setSelectedProcessingSteps} />
          : <div></div>
        }
      </Row>
      <Row>
        {(runId && datasetId)
          ? <ColumnInfo key='columnInfo' runId={runId} datasetId={datasetId} />
          : <div></div>
        }
      </Row>
    </Container>
  );
}
