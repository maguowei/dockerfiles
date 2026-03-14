# zsh-completions 补全路径必须在 oh-my-zsh 初始化之前加入 fpath
fpath=(/opt/zsh/zsh-completions/src $fpath)

# oh-my-zsh（内部自动调用 compinit，会感知上面设置的 fpath）
export ZSH=/opt/zsh/oh-my-zsh
ZSH_THEME=""
plugins=(git)
source $ZSH/oh-my-zsh.sh

# 补全插件（须在 oh-my-zsh 初始化后 source）
source /opt/zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# starship prompt
eval "$(starship init zsh)"

# zoxide（z 命令跳转目录）
eval "$(zoxide init zsh)"

# 工具别名
alias ls='eza --icons'
alias ll='eza -lh --icons --git'
alias la='eza -lah --icons --git'
alias lt='eza --tree --icons'
alias cat='bat --paging=never'
alias find='fd'
alias grep='rg'
