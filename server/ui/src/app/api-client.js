const endpoint = 'http://localhost:8080/'

export async function fetchColumnInfo(runId, datasetId){
    const url = new URL(endpoint + 'column-info/' + runId + '/' + datasetId);
    const response = await fetch(url);
    if (response.status === 200){
        const json = await response.json();
        console.log(json);
        return json;
    }
    return {};
}

export async function fetchRuns(){
    const url = new URL(endpoint + 'runs/');
    const response = await fetch(url);
    if (response.status === 200){
        const json = await response.json();
        return json;
    }
    return {};
}

export async function fetchRun(runId){
    const url = new URL(endpoint + 'runs/'+ runId);
    const response = await fetch(url);
    if (response.status == 200){
        const json = await response.json();
        return json;
    }
    return {};
}