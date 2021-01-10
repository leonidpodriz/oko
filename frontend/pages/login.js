import React from "react";
import Head from 'next/head';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { Button, TextField } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",

    "& > form": {
      display: "grid",
      gridGap: theme.spacing(4),
      width: '100%',
      maxWidth: "350px",
    }
  },
}));

const LoginPage = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Head>
        <title>Login</title>
      </Head>

      <h1>Log in to system</h1>

      <form>
        <TextField variant="outlined" label="Login" />+
        <TextField variant="outlined" label="Password" />
        <Button variant="contained" color="primary" disableElevation>Confirm</Button>

        <p>
          Don’t have account? <a href="#">Create account</a>
        </p>
      </form>
    </div>
  )
}

export default LoginPage;