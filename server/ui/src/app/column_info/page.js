'use client'

import Tab from 'react-bootstrap/Tab'
import Tabs from 'react-bootstrap/Tabs'
import StatTable from './statTable'
import { useEffect, useState } from 'react'
import { fetchColumnInfo } from '../api-client'

export default function ColumnInfo({runId, datasetId}){
    const [columnsByType, setColumnsByType] = useState({});

    useEffect(function(){
        if (runId && datasetId){
            fetchColumnInfo(runId, datasetId)
                .then(data => setColumnsByType(data));
        }
    }, [])
    
    if (Object.keys(columnsByType).length === 0){
        return <div></div>
    }
    else{
        return (
            <Tabs defaultActiveKey="stats" className='mb-3'>
                <Tab eventKey="stats" title="stats">
                {Object.keys(columnsByType).map(columnType => {
                    return <StatTable key={columnType} columnType={columnType} columnData={columnsByType[columnType]}/>
                })}
                </Tab>
                <Tab eventKey="plots" title="plots">
                    Plots
                </Tab>
            </Tabs>
        )
    }
}