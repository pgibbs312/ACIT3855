import logo from './stonks.jpg';
import './app.css';

import EndpointAudit from './components/EndpointAudit'
import AppStats from './components/AppStats'

function App() {

    const endpoints = ["stockNumber", "dateRange"]

    const rendered_endpoints = endpoints.map((endpoint) => {
        return <EndpointAudit key={endpoint} endpoint={endpoint}/>
    })

    return (
        <div className="app">
            <img src={logo} className="app-logo" alt="logo" height="300px" width="400px"/>
            <div>
                <AppStats/>
                <h1>Audit Endpoints</h1>
                {rendered_endpoints}
            </div>
        </div>
    );

}



export default app;