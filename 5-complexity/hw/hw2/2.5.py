from pyTM.MultiTM import MultiTM, MultiTMFactory, F, L, R, S, ANY

# 2.5.a
# ab -> c
q0,q1a,q1c,qa = 'q0','q1a','q1c','qa'
tm_a = (MultiTMFactory(2)
    .add_rule(q0, ('a','#'), qa, ('#'), (R, S))
    .add_rule(q0, ('b','#'), q0, ('b'), (R, R))
    .add_rule(q0, ('c','#'), q0, ('c'), (R, R))
    .add_rule(qa, ('b','#'), q0, ('c'), (R, R))
    .add_rule(qa, ('a','#'), q1a, ('a'), (S, R))
    .add_rule(qa, ('c','#'), q1c, ('a'), (S, R))
    .add_rule(q1a, ('a','#'), qa, ('#'), (R, S))
    .add_rule(q1c, ('c','#'), q0, ('c'), (R, S))
    .build(q0,[])
)
# tm_a.run("abcaabbcc", debug=False)


# 2.5.b
# abc -> aabbcc
q0,q1 = 'q0','q1'
tm_b = (MultiTMFactory(2)
    .add_rule(q0, ('a','#'), q1, ('a'), (S, R))
    .add_rule(q0, ('b','#'), q1, ('b'), (S, R))
    .add_rule(q0, ('c','#'), q1, ('c'), (S, R))
    .add_rule(q1, ('a','#'), q0, ('a'), (R, R))
    .add_rule(q1, ('b','#'), q0, ('b'), (R, R))
    .add_rule(q1, ('c','#'), q0, ('c'), (R, R))
    .build(q0,[])
)
# tm_b.run("abacbc")


# 2.5.c
# 0 1^x 0 1^y 0 -> 0 1^y 0 1^x 0
q0,q1 = 'q0','q1'
tm_c = (MultiTMFactory(2)
    .add_rule(q0, ('#','#'), q1, ('#'), (L, S))
    .add_rule(q0, (ANY,'#'), q0, ('#'), (R, S))
    .add_rule(q1, ('0','#'), q1, ('0'), (L, R))
    .add_rule(q1, ('1','#'), q1, ('1'), (L, R))
    .build(q0,[])
)
# tm_c.run('01111010')

# 2.5.d
q0, q1, q2,qr,qs = 'q0','q1','q2','qr','qs'
tm_d = (MultiTMFactory(2)
    .add_rule(q0, ('0','#'), q0, ('0'), (R, R))
    .add_rule(q0, ('1','#'), q0, ('1'), (R, R))
    .add_rule(q0, ('2','#'), qr, ('#'), (R, S))
    .add_rule(qr, ('#','#'), q1, ('#'), (L, L))
    .add_rule(qr, (ANY,'#'), qr, ('#'), (R, S))
    .add_rule(q1, ('0','0'), q1, ('0'), (L, L))
    .add_rule(q1, ('0','1'), q1, ('1'), (L, L))
    .add_rule(q1, ('1','0'), q1, ('1'), (L, L))
    .add_rule(q1, ('1','1'), q2, ('0'), (L, L))
    .add_rule(q2, ('1','1'), q2, ('1'), (L, L))
    .add_rule(q2, ('1','0'), q2, ('0'), (L, L))
    .add_rule(q2, ('0','1'), q2, ('0'), (L, L))
    .add_rule(q2, ('0','0'), q1, ('1'), (L, L))
    .add_rule(q2, ('0','#'), q1, ('1'), (L, L))
    .add_rule(q2, ('1','#'), q2, ('0'), (L, L))
    .add_rule(q1, ('0','#'), q1, ('0'), (L, L))
    .add_rule(q1, ('1','#'), q1, ('1'), (L, L))
    .add_rule(q1, ('2','#'), qs, ('#'), (S, L))
    .add_rule(q2, ('2','#'), qs, ('1'), (S, L))
    .build(q0,[])
)
tm_d.run('111210000')
