graph LR
    subgraph AFD para Number
        q0 -- dígito --> q1((q1));
        q1 -- dígito --> q1;
        q1 -- . --> q2;
        q2 -- dígito --> q3((q3));
        q3 -- dígito --> q3;
    end