"use client";

import { useState, useEffect } from "react";
import { FormGroup, FormSelect, Form } from "react-bootstrap";
import { fetchRuns } from "../api-client";

export default function RunSelection({ setRunId }) {
  const [runIds, setRunIds] = useState([]);

  const initRuns = () => {
    fetchRuns()
      .then(run_obj => {
        const runs = run_obj["runs"];
        if (runs.length !== 0){
          setRunId(runs[0]["run_id"]);
          runs.forEach(run => {
            setRunIds(oldRunIds => [...oldRunIds, run["run_id"]]);
          });
        }
      });
  }

  useEffect(function () {
    initRuns();
  }, []);

  return (
    <FormGroup>
      <Form.Label>Run ID</Form.Label>
      <FormSelect
        key="runIdFormSelect"
        aria-label='Select run ID'
        onChange={event => {
          event.preventDefault;
          setRunId(event.target.value)
        }}>
        {runIds.map(runId => {
          return <option key={runId} value={runId}>{runId}</option>
        })};
      </FormSelect>
    </FormGroup>

  );
}