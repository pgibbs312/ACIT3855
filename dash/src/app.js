import logo from './logo.webp';
import './app.css';

import EndpointAudit from './components/endpointAudit'
import AppStats from './components/appStats'

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



export default App;