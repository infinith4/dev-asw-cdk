```
python --version

cdk --version

cd deploy_src/

source .venv/bin/activate

python -m pip install -r requirements.txt
```

```
(.venv) vscode ? /src/deploy_src $ cdk ls
AppRunnerServiceStack
```

https://dev.classmethod.jp/articles/cdk-supports-sso-profile/

IAM Identity Center

でユーザを作成し、AdministratorAccess を付与する。

```
aws configure sso
```

```
(.venv) vscode ➜ /src/deploy_src $ aws configure sso
SSO session name (Recommended): dev-aws-cdk-user-sso
SSO start URL [None]: https://xxxxxxxxxxx.awsapps.com/start/
SSO region [None]: ap-northeast-1
SSO registration scopes [sso:account:access]:
Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

https://oidc.ap-northeast-1.amazonaws.com/authorize?XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

```
aws sts get-caller-identity --profile [Profile name]
```

```
aws sso login --profile [Profile name]
```

```
cdk bootstrap  --profile [Profile name]
```

```
(.venv) vscode ? /src/deploy_src $ cdk bootstrap  --profile [Profile name]
 ?  Bootstrapping environment aws://[Account Id]/ap-northeast-1...
Trusted accounts for deployment: (none)
Trusted accounts for lookup: (none)
Using default execution policy of 'arn:aws:iam::aws:policy/AdministratorAccess'. Pass '--cloudformation-execution-policies' to customize.
CDKToolkit: creating CloudFormation changeset...
 ?  Environment aws://[Account Id]/ap-northeast-1 bootstrapped.
```

```
aws sts get-caller-identity --profile [Profile name]
```


```
cdk deploy --profile [Profile name]
```


