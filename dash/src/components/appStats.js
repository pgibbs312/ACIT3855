import React, { useEffect, useState } from 'react'
import '../app.css';

export default function appStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://pg-acit3855-kafka.eastus.cloudapp.azure.com:8100/game/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (
        <div className={"error"}>
            <p>Error found when fetching from API</p>
            <table className={"statsTable"}>
                <tbody>
                    <tr>
                        <th>Service Status</th>
                    </tr>
                    <tr>
                        <td colspan="2">Receiver: {health['receiver']}</td>
                    </tr>
                    <tr>
                        <td colspan="2">Storage: {health['storage']}</td>
                    </tr>
                    <tr>
                        <td colspan="2">Processing: {health['processing']}</td>
                    </tr>
                    <tr>
                        <td colspan="2">Audit: {health['audit']}</td>
                    </tr>
                    <tr>
                        <td colspan="2">Last Updated: {health['last_updated']}</td>
                    </tr>
                </tbody>
            </table>
        </div>
                
        )
    }
    else if (isLoaded === false){
        return(<div>Loading...</div>)
    } 
    else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"statsTable"}>
					<tbody>
						<tr>
							<th>Users</th>
							<th>Scores</th>
						</tr>
						<tr>
							<td>Count: {stats['num_users']}</td>
							<td>Count: {stats['num_scores']}</td>
						</tr>
						<tr>
							<td colspan="2">Top Score: {stats['top_score']}</td>
						</tr>
						<tr>
							<td colspan="2">Lowest Score: {stats['low_score']}</td>
						</tr>
						<tr>
							<td colspan="2">Longest Run: {stats['longest_run']}</td>
						</tr>
                        <tr>
							<td colspan="2">Shortest Run: {stats['shortest_run']}</td>
						</tr>
					</tbody>
                </table>
                <table className={"statsTable"}>
					<tbody>
						<tr>
							<th>Service Status</th>
						</tr>
						<tr>
							<td colspan="2">Receiver: {health['receiver']}</td>
						</tr>
						<tr>
							<td colspan="2">Storage: {health['storage']}</td>
						</tr>
						<tr>
							<td colspan="2">Processing: {health['processing']}</td>
						</tr>
                        <tr>
							<td colspan="2">Audit: {health['audit']}</td>
						</tr>
                        <tr>
							<td colspan="2">Last Updated: {health['last_updated']}</td>
						</tr>
					</tbody>
                </table>
        
                
                
                {/* <h3>Last Updated: {stats['last_updated']}</h3> */}

            </div>
        )
    }
    
}