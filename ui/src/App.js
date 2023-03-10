import './App.css';

import {useState, useEffect} from 'react';
import axios from 'axios';

function App() {

    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {

        setLoading(true);

        axios
            .get("http://localhost:8080/v2/beta/hello")
            .then((result) => {
                setData(result.data.message);
                setLoading(false);
            })
            .catch((error) => console.log(error));
        }, []);

    if (loading) {
        return <p>Loading...</p>
    }

    console.log("data=" + data);

    return (
        <div className="container">
            <p>{data}</p>
        </div>
    );

}

export default App;
