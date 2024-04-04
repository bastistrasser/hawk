'use client'

import { Table } from 'react-bootstrap'

export default function StatTable({columnType, columnData}){
    if (!columnData){
        return <div key={["stats", "-", columnType].join()}></div>
    }
    else{
        return (
            <div key={["stats", "-", columnType].join()}>
                <h2>{columnType}</h2>
                <Table bordered>
                    <thead key="thead">
                        <tr key="header">
                        {columnData['header'].map(function(header, indexHeader) {
                            return <th key={header}>{header}</th>
                        })}
                        </tr>
                    </thead>
                    <tbody key="tbody">
                        {columnData['metadata'].map(function(column, indexColumn) {
                            return <tr key={indexColumn}>
                                {column.map(function(stat, indexStat){
                                    return <td key={['stat', '-', indexColumn, '-', indexStat].join()}>{stat}</td>
                                })}
                            </tr>
                        })}
                    </tbody>
                </Table>
            </div>

        )
    }
}