import Head from 'next/head'
import { useEffect, useState } from 'react'
import styles from '../styles/Home.module.css'

export default function Home() {
  const [status, setStatus] = useState("loading");
  useEffect(() => fetch("http://localhost:8000/").then(data => data.json()).then(data => setStatus(data.status)), [])




  return (
    <div className={styles.container}>
      <Head>
        <title>Single</title>
      </Head>

      <pre>Status: {status}</pre>
    </div>
  )
}
