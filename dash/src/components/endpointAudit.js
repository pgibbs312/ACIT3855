import React, { useEffect, useState } from 'react'
import '../app.css';

export default function EndpointAudit(props) {
    console.log(`props is: ${props}`);
    const [isLoaded, setIsLoaded] = useState(false);
    const [log, setLog] = useState(null);
    const [error, setError] = useState(null)
	const rand_val = Math.floor(Math.random() * 100); // Get a random event from the event store
    const [index, setIndex] = useState(null); //state for index

    const getAudit = () => {
        fetch(`pg-acit3855-kafka.eastus.cloudapp.azure.com/game/score?index=${rand_val}`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Audit Results for " + props.endpoint)
                setLog(result);
                setIsLoaded(true);
                setIndex(rand_val);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
	useEffect(() => {
		const interval = setInterval(() => getAudit(), 4000); // Update every 4 seconds
		return() => clearInterval(interval);
    }, [getAudit]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        
        return ( 
            <div> 
                <h3>{props.endpoint}-{index}</h3> 
                {JSON.stringify(log)} 
            </div> 
        )
    }
}