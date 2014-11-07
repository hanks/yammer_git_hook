Git hook for sending yammer message
=============================

A self-use tool for detecting git merge and push action to send yammer message to group


## Why
Because during my job, there is a workflow that when you merge a branch to develop, you need to send yammer message to group to notify other members in the team, the easy tool is created.

## Demo
![alt text][demo]

[demo]: https://raw.githubusercontent.com/hanks/yammer_git_hook/master/resources/demo.gif "demo"

**The result will be:**

![alt text][result]

[result]: https://raw.githubusercontent.com/hanks/yammer_git_hook/master/resources/result.png "result"

## Implementation
Mainly two points:

<ol>
  <li>git hook</li>
    <ol>
      <li>pre-push to detecting git push action.</li>
      <li>prepare-commit-msg to detecting git merge action</li>
      <li>you can find more about git hook in <a href="http://git-scm.com/book/en/Customizing-Git-Git-Hooks">Git Hook</a></li>
    </ol>
  <li>yammer oauth    
    <ol>
      <li>You can find more infomation in <a href="http://developer.yammer.com/authentication/">Yammer OAuth.</a></li>
  </li>
    </ol>
  </li>                
</ol>

## Be Careful
With security considerations, there are some hard-codings in the code, like client\_id, access\_token in local.settings. But the source code is easy. 

To the yammer oauth part, you just need to get access_token firstly, and to post you message with auth header info in your request.

To the git hook part, there may be **some problems** need to be solved:
<ol>
  <li>git hook is easy to not to be executed because of conflicts, here I can do is just to use git pull and git merge --no-ff as often as possible to trigger the hook and need god bless.</li>    
  <li>if git hook failed during execution, it will affect the main git operations, like push or merge fail, You need to be careful about this one. Or else this will influence your job...</li>
</ol>


## Install
It needs to be install from both git and yammer side.
<ol>
  <li>Git hook part</li>
    <ol>
      <li>Just put git hook shell script file to .git/hooks folder</li>
    </ol>
  <li>Yammer part      
    <ol>
      <li>Register you app with your account to get cliend_id and redirect_url</li>
      <li>Use cliend_id to access auth url in browser and get access_token in the redirect_url after authenticating your app</li>
      <li>Use access_token with <a href="http://developer.yammer.com/restapi/">Yammer REST API</a> to do what you want</li>
    </ol>
  </li>                
</ol>

## Usage
1. ./client.py -g # to show group id info<br />
2. ./client.py msg\_part\_1 msg\_part\_2 # to send message to specified group id

## Contribution
**Waiting for your pull request, may be hard to reuse...**

## Lisence
MIT Lisence
