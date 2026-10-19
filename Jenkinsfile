pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
    }

    environment {
        PYTHONIOENCODING = 'utf-8'
        PYTHONUNBUFFERED = '1'
        PIP_INDEX_URL    = 'https://pypi.tuna.tsinghua.edu.cn/simple'
        PIP_TRUSTED_HOST = 'pypi.tuna.tsinghua.edu.cn'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    tools {
        jdk 'jdk8'
    }

    stages {
        stage('Prepare') {
            steps {
                bat '''
                    if exist .venv rmdir /s /q .venv
                    python -m venv .venv
                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                bat '''
                    if exist reports rmdir /s /q reports
                    if exist allure-results rmdir /s /q allure-results
                    mkdir reports
                    mkdir allure-results
                    .venv\\Scripts\\python.exe -m pytest -v --junitxml=reports/junit.xml --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            // 第 1 步：先把测试结果发布给 Jenkins，必须在清理之前执行
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            // 第 6 步配好 Allure 命令行工具后再打开下面这行
            // allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            // 第 2 步：清理构建现场（虚拟环境 + 缓存目录）
            echo '清理虚拟环境和临时文件'
            bat '''
                if exist .venv rmdir /s /q .venv
                if exist .pytest_cache rmdir /s /q .pytest_cache
                for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
                exit /b 0
            '''
        }
        success {
            echo '全部用例通过'
        }
        failure {
            echo '存在失败用例，请查看上方日志和测试报告'
        }
    }
}
